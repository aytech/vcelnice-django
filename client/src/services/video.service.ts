import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';
import { Video } from 'interfaces';


@Injectable()
export class VideoService {

  constructor(
    private http: HttpClient
  ) {
  }

  getVideos(): Observable<Array<Video>> {
    return this.http.get<Video[]>(ApiConstants.GET_VIDEOS);
  }
}
