import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { PrivacyComponent } from '../privacy/privacy.component'

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FooterComponent {
  private readonly modalService = inject(NgbModal)

  openPrivacy(event: MouseEvent): void {
    if (
      event.defaultPrevented
      || event.button !== 0
      || event.ctrlKey
      || event.metaKey
      || event.shiftKey
      || event.altKey
    ) {
      return
    }

    event.preventDefault()
    this.modalService.open(PrivacyComponent, {
      ariaDescribedBy: 'privacy-modal-intro',
      ariaLabelledBy: 'privacy-modal-title',
      backdropClass: 'privacy-modal-backdrop',
      centered: true,
      fullscreen: 'sm',
      scrollable: true,
      size: 'lg',
      windowClass: 'privacy-modal'
    })
  }
}
