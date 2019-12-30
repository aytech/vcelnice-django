import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { PriceService, GenericService, LanguageService } from 'services';
import { Culture, PickLocation, Price } from 'interfaces';

@Component({
  selector: 'app-prices',
  templateUrl: './prices.component.html',
  styleUrls: ['./prices.component.css']
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
    const modalRef = this.modalService.open(ReservationComponent);
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
  templateUrl: './reservation.component.html',
  styleUrls: ['./prices.component.css']
})
export class ReservationComponent implements OnInit {

  @ViewChild('form') form: NgForm;
  @Input() title: string;
  @Input() amount_description: string;
  private csrf_token: string;
  public isSubmitting: boolean;
  public hasError: boolean;
  public hasSuccess: boolean;
  private readonly language: string;
  public postMessage: string;
  public locations: Array<PickLocation>;
  public cultures: Culture;

  constructor(
    public activeModal: NgbActiveModal,
    private priceService: PriceService,
    private genericService: GenericService,
    private languageService: LanguageService
  ) {
    this.isSubmitting = false;
    this.hasError = false;
    this.hasSuccess = false;
  }

  ngOnInit() {
    this.cultures = this.languageService.cultures;
    this.priceService.getLocations()
      .subscribe((locations) => {
        this.locations = locations;
      }, (error: HttpErrorResponse) => {
        console.error('Error fetching data: ', error.statusText);
      });
    this.genericService.getCSRFToken().subscribe((response: string) => {
      this.csrf_token = response;
    });
    this.languageService.language.subscribe(() => {
      this.cultures = this.languageService.cultures;
    });
  }

  send(): void {
    this.isSubmitting = true;
    this.hasError = false;
    this.hasSuccess = false;
    this.form.value.title = this.title;

    this.priceService.postReservation(this.form.value, this.language, this.csrf_token)
      .subscribe(() => {
          this.hasSuccess = true;
          this.isSubmitting = false;
          this.postMessage = this.cultures.reservation_ok;
          this.form.reset();
          this.form.controls.location.setValue('');
        }, () => {
          this.hasError = true;
          this.isSubmitting = false;
          this.postMessage = this.cultures.server_error;
        }
      );
  }
}
