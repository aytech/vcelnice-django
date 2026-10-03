import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'
import { Video } from '@interfaces'

import { VideoService } from './video.service'

describe('VideoService', () => {
  let service: VideoService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        VideoService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(VideoService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads videos from the API response', () => {
    const videos: Video[] = [{
      youtube_id: 'dQw4w9WgXcQ',
      caption: 'Apiary video',
      description: null,
      thumb: null
    }]
    let result: typeof videos | undefined

    service.getVideos().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_VIDEOS
    })
    request.flush({ videos })

    expect(result).toEqual(videos)
  })
})
