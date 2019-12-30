import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';
import { Home } from 'interfaces';

@Injectable()
export class HomeService {

  constructor(
    private http: HttpClient) {
  }

  getText(): Observable<Home> {
    return this.http.get<Home>(ApiConstants.GET_HOME);
  }
}
