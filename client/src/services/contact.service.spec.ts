import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'

import { ContactService } from './contact.service'

describe('ContactService', () => {
  let service: ContactService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ContactService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(ContactService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('posts a contact message with locale and CSRF headers', () => {
    const data = { name: 'Visitor', message: 'Hello' }
    const response = { sent: true }
    let result: typeof response | undefined

    service.postMessage(data, 'en', 'csrf-token')
      .subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'POST',
      url: ApiConstants.POST_CONTACT
    })
    expect(request.request.body).toEqual(data)
    expect(request.request.headers.get('Accept-Language')).toBe('en')
    expect(request.request.headers.get('X-CSRFToken')).toBe('csrf-token')
    request.flush(response)

    expect(result).toEqual(response)
  })
})
