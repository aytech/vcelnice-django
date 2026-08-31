import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal
} from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { LanguageService, PriceService } from '@services'
import { Price } from '@interfaces'

@Component({
  selector: 'app-prices',
  templateUrl: './prices.component.html',
  styleUrls: ['./prices.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PricesComponent {

  private readonly modalService = inject(NgbModal)
  private readonly priceService = inject(PriceService)
  private readonly languageService = inject(LanguageService)

  readonly cultures = this.languageService.culturesSignal
  readonly pricesResource = rxResource({
    stream: () => this.priceService.getPrices()
  })

  openReservationForm(price: Price): void {
    const modalRef = this.modalService.open(ReservationModalComponent)
    const amountDescription = price.amount_description
      ?? this.cultures().amount_description

    const reservation = modalRef.componentInstance as ReservationModalComponent
    reservation.title.set(price.title)
    reservation.amountDescription.set(amountDescription)
  }
}

@Component({
  selector: 'reservation',
  templateUrl: './reservation.modal.html',
  styleUrls: ['./prices.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReservationModalComponent {

  readonly title = signal('')
  readonly amountDescription = signal('')
  readonly cultures = inject(LanguageService).culturesSignal

  constructor(public readonly activeModal: NgbActiveModal) { }
}
