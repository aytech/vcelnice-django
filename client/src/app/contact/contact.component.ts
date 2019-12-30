import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { NgForm } from '@angular/forms';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ContactService, GenericService, LanguageService } from 'services';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {

  constructor(private modalService: NgbModal) {
  }

  ngOnInit() {
  }

  openContactForm(): void {
    this.modalService.open(ContactModalComponent);
  }
}

@Component({
  selector: 'reservation',
  templateUrl: './contact.modal.html',
  styleUrls: ['./contact.component.css']
})
export class ContactModalComponent implements OnInit {

  @ViewChild('form') form: NgForm;
  private csrf_token: string;
  public emailErrorMessage: string;
  public contactFormTitle: string;
  public isSubmitting: boolean;
  public hasError: boolean;
  public hasSuccess: boolean;
  public postMessage: string;

  constructor(
    public activeModal: NgbActiveModal,
    private contactService: ContactService,
    private genericService: GenericService,
    private route: ActivatedRoute,
    private languageService: LanguageService
  ) {
    this.emailErrorMessage = languageService.cultures.error_empty_message;
    this.contactFormTitle = languageService.cultures.contact_form;
    this.isSubmitting = false;
    this.hasError = false;
    this.hasSuccess = false;
  }

  ngOnInit() {
    this.genericService.getCSRFToken().subscribe((response: string) => {
      this.csrf_token = response;
    });
  }

  send(): void {
    this.isSubmitting = true;
    this.hasError = false;
    this.hasSuccess = false;

    const locale = this.languageService.locale;
    this.contactService.postMessage(this.form.value, locale, this.csrf_token)
      .subscribe(
        () => {
          this.hasSuccess = true;
          this.isSubmitting = false;
          this.postMessage = this.languageService.cultures.ok_message_sent;
          this.form.reset();
        }, (reason: HttpErrorResponse) => {
          this.hasError = true;
          this.isSubmitting = false;
          for (const error in reason.error) {
            if (reason.error.hasOwnProperty(error)) {
              this.postMessage = reason.error[error][0];
            }
          }
        }
      );
  }
}
