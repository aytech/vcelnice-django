import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'
import { Article } from '@interfaces'

import { NewsService } from './news.service'

describe('NewsService', () => {
  let service: NewsService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        NewsService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(NewsService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads news from the API response', () => {
    const news: Article[] = [{
      id: 1,
      title: 'Harvest',
      text: 'Honey harvest update',
      icon: 'honey',
      created: '2026-10-01T10:00:00Z',
      updated: '2026-10-02T10:00:00Z'
    }]
    let result: typeof news | undefined

    service.getNews().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_NEWS
    })
    request.flush({ news })

    expect(result).toEqual(news)
  })
})
