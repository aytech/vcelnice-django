import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';
import { Certificate } from 'interfaces';


@Injectable()
export class CertificateService {

  constructor(
    private http: HttpClient
  ) {
  }

  getCertificates(): Observable<Array<Certificate>> {
    return this.http.get<Certificate[]>(ApiConstants.GET_CERTIFICATES);
  }
}
