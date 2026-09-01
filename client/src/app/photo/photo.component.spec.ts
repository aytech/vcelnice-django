import { ComponentFixture, TestBed } from '@angular/core/testing'
import { Subject } from 'rxjs'
import { Photo } from '@interfaces'
import { PhotoService } from '@services'
import { PhotoComponent } from './photo.component'

describe('PhotoComponent', () => {
  let fixture: ComponentFixture<PhotoComponent>
  let photoResponse: Subject<Photo[]>
  let photoService: jasmine.SpyObj<PhotoService>

  beforeEach(async () => {
    photoResponse = new Subject<Photo[]>()
    photoService = jasmine.createSpyObj<PhotoService>('PhotoService', ['getPhotos'])
    photoService.getPhotos.and.returnValue(photoResponse)

    await TestBed.configureTestingModule({
      declarations: [PhotoComponent],
      providers: [{ provide: PhotoService, useValue: photoService }]
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

  it('shows eight previews while registering every photo in the gallery', async () => {
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
      element.querySelectorAll<HTMLAnchorElement>(
        'a[data-fancybox="photo-gallery"]'
      )
    )
    const hiddenGalleryLinks = galleryLinks.filter(link => link.hidden)

    expect(previews).toHaveSize(8)
    expect(previews.map(preview => preview.querySelector('.card-title')?.textContent?.trim()))
      .toEqual(photos.slice(0, 8).map(photo => photo.caption))
    expect(galleryLinks).toHaveSize(photos.length)
    expect(galleryLinks.map(link => link.getAttribute('href')))
      .toEqual(photos.map(photo => photo.image))
    expect(galleryLinks.map(link => link.getAttribute('data-caption')))
      .toEqual(photos.map(photo => photo.caption))
    expect(hiddenGalleryLinks).toHaveSize(photos.length - 8)
    expect(hiddenGalleryLinks.every(link => link.tabIndex === -1)).toBeTrue()
    expect(hiddenGalleryLinks.every(link => link.getAttribute('aria-hidden') === 'true'))
      .toBeTrue()
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    photoResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
