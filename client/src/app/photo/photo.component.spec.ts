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

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    photoResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
