import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { HomeService, NewsService } from 'services';
import { forkJoin } from 'rxjs';
import {
  Article,
  Home
} from 'interfaces';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    standalone: false
})
export class HomeComponent implements OnInit {

  public home: Home;
  public articles: Array<Article>;
  public loading: boolean;
  public error: boolean;

  constructor(
    private homeService: HomeService,
    private newsService: NewsService
  ) {
    this.articles = [];
    this.loading = true;
    this.error = false;
  }

  ngOnInit() {
    const home = this.homeService.getText();
    const news = this.newsService.getNews();

    forkJoin([home, news])
      .subscribe((response: [Home, Article[]]) => {
          this.loading = false;
          this.home = response[0];
          this.articles = response[1].slice(0, 4);
        },
        (error: HttpErrorResponse) => {
          this.loading = false;
          this.error = true;
          console.error('Error fetching data: ', error.statusText);
        });
  }
}
