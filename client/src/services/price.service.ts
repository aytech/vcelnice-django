import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { map, Observable } from 'rxjs'
import { ApiConstants } from '@config'
import { Location, Price } from '@interfaces'


@Injectable()
export class PriceService {

  constructor(
    private http: HttpClient
  ) {
  }

  getPrices(): Observable<Price[]> {
    return this.http
      .get<{prices: Price[]}>(ApiConstants.GET_PRICES)
      .pipe(map(response => response.prices))
  }

  getLocations(): Observable<Array<Location>> {
    return this.http.get<Array<Location>>(ApiConstants.GET_LOCATIONS)
  }

  postReservation(data: any, lang: string, token: string): Observable<any> {
    return this.http.post(ApiConstants.POST_RESERVATION, data, {
      headers: new HttpHeaders()
        .set('Accept-Language', lang)
        .set('X-CSRFToken', token)
    });
  }
}
