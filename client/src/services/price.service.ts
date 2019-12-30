import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';
import { Location, Price } from 'interfaces';


@Injectable()
export class PriceService {

  constructor(
    private http: HttpClient
  ) {
  }

  getPrices(): Observable<Array<Price>> {
    return this.http.get<Array<Price>>(ApiConstants.GET_PRICES);
  }

  getLocations(): Observable<Array<Location>> {
    return this.http.get<Array<Location>>(ApiConstants.GET_LOCATIONS);
  }

  postReservation(data: any, lang: string, token: string): Observable<any> {
    return this.http.post(ApiConstants.POST_RESERVATION, data, {
      headers: new HttpHeaders()
        .set('Accept-Language', lang)
        .set('X-CSRFToken', token)
    });
  }
}
