import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { map, Observable } from 'rxjs'
import { ApiConstants } from '@config'
import { Certificate } from '@interfaces'


@Injectable()
export class CertificateService {

  constructor(
    private http: HttpClient
  ) {
  }

  getCertificates(): Observable<Certificate[]> {
    return this.http
      .get<{certificates: Certificate[]}>(ApiConstants.GET_CERTIFICATES)
      .pipe(map(response => response.certificates))
  }
}
