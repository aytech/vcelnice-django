import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'

import { GenericService } from './generic.service'

describe('GenericService', () => {
  let service: GenericService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        GenericService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(GenericService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads the CSRF token', () => {
    let result: string | undefined

    service.getCSRFToken().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_CSRF_TOKEN
    })
    request.flush('csrf-token')

    expect(result).toBe('csrf-token')
  })
})
