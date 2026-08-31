import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { NewsService } from '@services'

@Component({
    selector: 'app-news',
    templateUrl: './news.component.html',
    styleUrls: ['./news.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class NewsComponent {

  private readonly newsService = inject(NewsService)

  readonly articlesResource = rxResource({
    stream: () => this.newsService.getNews()
  })
}
