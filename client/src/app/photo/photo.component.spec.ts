import { ComponentFixture, TestBed } from '@angular/core/testing'
import { By } from '@angular/platform-browser'
import { Subject } from 'rxjs'
import { Photo } from '@interfaces'
import { PhotoService } from '@services'
import { LightboxService } from '../shared/lightbox/lightbox.service'
import { PhotoComponent } from './photo.component'

describe('PhotoComponent', () => {
  let fixture: ComponentFixture<PhotoComponent>
  let photoResponse: Subject<Photo[]>
  let photoService: jasmine.SpyObj<PhotoService>
  let lightbox: jasmine.SpyObj<LightboxService>

  beforeEach(async () => {
    photoResponse = new Subject<Photo[]>()
    photoService = jasmine.createSpyObj<PhotoService>('PhotoService', ['getPhotos'])
    photoService.getPhotos.and.returnValue(photoResponse)
    lightbox = jasmine.createSpyObj<LightboxService>('LightboxService', ['openPhotos'])

    await TestBed.configureTestingModule({
      declarations: [PhotoComponent],
      providers: [
        { provide: PhotoService, useValue: photoService },
        { provide: LightboxService, useValue: lightbox }
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(PhotoComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const photo: Photo = {
      id: 1,
      image: '/media/apiary.jpg',
      caption: 'Včelnice v létě',
      thumb: '/media/apiary-thumb.jpg'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    photoResponse.next([photo])
    photoResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('.card-title')?.textContent).toContain(photo.caption)
  })

  it('shows eight previews and opens the complete gallery at the selected photo', async () => {
    const photos: Photo[] = Array.from({length: 12}, (_, index) => ({
      id: index + 1,
      image: `/media/photo-${index + 1}.jpg`,
      caption: `Fotografie ${index + 1}`,
      thumb: index === 2 ? '' : `/media/photo-${index + 1}-thumb.jpg`
    }))

    photoResponse.next(photos)
    photoResponse.complete()
    await fixture.whenStable()

    const element: HTMLElement = fixture.nativeElement
    const previews = Array.from(
      element.querySelectorAll<HTMLElement>('.card-container')
    )
    const galleryLinks = Array.from(
      element.querySelectorAll<HTMLAnchorElement>('a.thumbnail')
    )

    expect(previews).toHaveSize(8)
    expect(previews.map(preview => preview.querySelector('.card-title')?.textContent?.trim()))
      .toEqual(photos.slice(0, 8).map(photo => photo.caption))
    expect(galleryLinks).toHaveSize(8)
    expect(galleryLinks.map(link => link.getAttribute('href')))
      .toEqual(photos.slice(0, 8).map(photo => photo.image))
    expect(galleryLinks[2].querySelector('img')?.getAttribute('src'))
      .toBe('/assets/images/default.png')
    expect(galleryLinks[2].querySelector('img')?.alt).toBe(photos[2].caption)
    expect(element.querySelector('a[hidden]')).toBeNull()

    const event = new MouseEvent('click', { button: 0, cancelable: true })
    fixture.debugElement.queryAll(By.css('a.thumbnail'))[5].triggerEventHandler('click', event)

    expect(lightbox.openPhotos).toHaveBeenCalledOnceWith(event, photos, 5)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    photoResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
