import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { LanguageService } from '@services'

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FooterComponent {

  readonly language = inject(LanguageService).localeSignal
}
