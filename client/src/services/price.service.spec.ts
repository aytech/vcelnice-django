import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'

import { PriceService } from './price.service'

describe('PriceService', () => {
  let service: PriceService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        PriceService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(PriceService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads prices from the API response', () => {
    const prices = [{
      amount_description: 'Jar',
      id: 1,
      image: '/media/honey.jpg',
      in_store: 2,
      price: '150',
      title: 'Honey',
      weight: '500 g'
    }]
    let result: typeof prices | undefined

    service.getPrices().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_PRICES
    })
    request.flush({ prices })

    expect(result).toEqual(prices)
  })

  it('loads reservation pickup locations', () => {
    const locations = [{ address: 'Apiary 1' }]
    let result: typeof locations | undefined

    service.getLocations().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_LOCATIONS
    })
    request.flush(locations)

    expect(result).toEqual(locations)
  })

  it('posts a reservation with language and CSRF headers', () => {
    const data = { price: 1, amount: 2 }
    const response = { reserved: true }
    let result: typeof response | undefined

    service.postReservation(data, 'cs', 'csrf-token')
      .subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'POST',
      url: ApiConstants.POST_RESERVATION
    })
    expect(request.request.body).toEqual(data)
    expect(request.request.headers.get('Accept-Language')).toBe('cs')
    expect(request.request.headers.get('X-CSRFToken')).toBe('csrf-token')
    request.flush(response)

    expect(result).toEqual(response)
  })
})
