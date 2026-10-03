import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'
import { Photo } from '@interfaces'

import { PhotoService } from './photo.service'

describe('PhotoService', () => {
  let service: PhotoService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        PhotoService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(PhotoService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads photos from the API response', () => {
    const photos: Photo[] = [{
      id: 1,
      image: '/media/photo.jpg',
      caption: 'Apiary',
      thumb: '/media/photo-thumb.jpg'
    }]
    let result: typeof photos | undefined

    service.getPhotos().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_PHOTOS
    })
    request.flush({ photos })

    expect(result).toEqual(photos)
  })
})
