import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { HomeService, NewsService } from '@services'
import { forkJoin, map } from 'rxjs'
import {
  Article,
  Home
} from '@interfaces'

interface HomePage {
  home: Home
  articles: Article[]
}

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent {

  private readonly homeService = inject(HomeService)
  private readonly newsService = inject(NewsService)

  readonly pageResource = rxResource({
    stream: () => forkJoin({
      home: this.homeService.getText(),
      articles: this.newsService.getNews()
    }).pipe(
      map(({home, articles}): HomePage => ({
        home,
        articles: articles.slice(0, 4)
      }))
    )
  })
}
