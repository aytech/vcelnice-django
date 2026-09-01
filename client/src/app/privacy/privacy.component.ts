import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'

@Component({
  selector: 'app-privacy',
  templateUrl: './privacy.component.html',
  styleUrls: ['./privacy.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PrivacyComponent {
  private readonly activeModal = inject(NgbActiveModal, {optional: true})

  readonly isModal = this.activeModal !== null
  readonly titleId = this.isModal ? 'privacy-modal-title' : 'privacy-page-title'
  readonly introId = this.isModal ? 'privacy-modal-intro' : 'privacy-page-intro'

  dismissModal(): void {
    this.activeModal?.dismiss('Cross click')
  }

  closeModal(): void {
    this.activeModal?.close('Close click')
  }

  closeForNavigation(): void {
    this.activeModal?.close('Contact link')
  }
}
