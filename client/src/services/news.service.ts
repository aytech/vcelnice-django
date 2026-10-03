import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { map, Observable, pipe } from 'rxjs'
import { ApiConstants } from '@config'
import { Article } from '@interfaces'

@Injectable()
export class NewsService {

  constructor(
    private http: HttpClient) {
  }

  getNews(): Observable<Array<Article>> {
    return this.http
      .get<{news: Article[]}>(ApiConstants.GET_NEWS)
      .pipe(map(response => response.news))
  }
}
