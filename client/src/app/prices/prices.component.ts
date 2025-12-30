import { Component, OnInit, Input } from '@angular/core'
import { HttpErrorResponse } from '@angular/common/http';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { PriceService, LanguageService } from 'services';
import { Culture, Price } from 'interfaces';

@Component({
  selector: 'app-prices',
  templateUrl: './prices.component.html',
  styleUrls: ['./prices.component.css'],
  standalone: false
})
export class PricesComponent implements OnInit {

  public loading: boolean;
  public prices: Array<Price>;
  public cultures: Culture;

  constructor(
    private modalService: NgbModal,
    private priceService: PriceService,
    private languageService: LanguageService
  ) {
    this.loading = true;
    this.prices = [];
  }

  ngOnInit() {
    this.cultures = this.languageService.cultures;
    this.priceService.getPrices()
      .subscribe(prices => {
        this.loading = false;
        this.prices = prices;
      }, (error: HttpErrorResponse) => {
        this.loading = false;
        console.error('Error fetching data: ', error.statusText);
      });
    this.languageService.language.subscribe(() => {
      this.cultures = this.languageService.cultures;
    });
  }

  openReservationForm(index: number): void {
    const price: Price = this.prices[index];
    const modalRef = this.modalService.open(ReservationModalComponent);
    let amount_description = price.amount_description;
    if (amount_description === null || amount_description === undefined) {
      amount_description = this.cultures.amount_description;
    }
    modalRef.componentInstance.title = price.title;
    modalRef.componentInstance.amount_description = amount_description;
  }
}

@Component({
  selector: 'reservation',
  templateUrl: './reservation.modal.html',
  styleUrls: ['./prices.component.css'],
  standalone: false
})
export class ReservationModalComponent implements OnInit {

  @Input() title: string;
  public cultures: Culture;

  constructor(
    public activeModal: NgbActiveModal,
    private languageService: LanguageService
  ) { }

  ngOnInit() {
    this.cultures = this.languageService.cultures;

    this.languageService.language.subscribe(() => {
      this.cultures = this.languageService.cultures;
    });
  }
}
