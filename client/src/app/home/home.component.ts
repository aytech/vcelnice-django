import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { HomeService } from '@services'

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent {

  private readonly homeService = inject(HomeService)

  readonly homeResource = rxResource({
    stream: () => this.homeService.getText()
  })
}
