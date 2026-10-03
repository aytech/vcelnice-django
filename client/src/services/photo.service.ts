import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { map, Observable } from 'rxjs'
import { ApiConstants } from '@config'
import { Photo } from '@interfaces'

@Injectable()
export class PhotoService {

  constructor(
    private http: HttpClient
  ) {
  }

  getPhotos(): Observable<Array<Photo>> {
    return this.http
      .get<{photos: Photo[]}>(ApiConstants.GET_PHOTOS)
      .pipe(map(response => response.photos))
  }
}
