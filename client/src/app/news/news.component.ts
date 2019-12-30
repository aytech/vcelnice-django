import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { NewsService } from 'services';
import { Article } from 'interfaces';

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent implements OnInit {

  public articles: Array<Article>;
  public loading: boolean;

  constructor(private newsService: NewsService) {
    this.loading = true;
    this.articles = [];
  }

  ngOnInit() {
    this.newsService.getNews()
      .subscribe((response: Article[]) => {
          this.loading = false;
          this.articles = response;
        },
        (error: HttpErrorResponse) => {
          this.loading = false;
          console.error('Error fetching data: ', error.statusText);
        });
  }
}
