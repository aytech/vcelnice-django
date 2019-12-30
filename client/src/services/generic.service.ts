import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';


@Injectable()
export class GenericService {

  constructor(
    private http: HttpClient
  ) { }

  getCSRFToken(): Observable<any> {
    return this.http.get<string>(ApiConstants.GET_CSRF_TOKEN);
  }
}
