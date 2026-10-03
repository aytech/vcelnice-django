import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'

import { CertificateService } from './certificate.service'

describe('CertificateService', () => {
  let service: CertificateService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CertificateService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(CertificateService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads certificates from the API response', () => {
    const certificates = [{
      file: '/media/certificate.pdf',
      description: 'Quality certificate',
      type: 'pdf'
    }]
    let result: typeof certificates | undefined

    service.getCertificates().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_CERTIFICATES
    })
    request.flush({ certificates })

    expect(result).toEqual(certificates)
  })
})
