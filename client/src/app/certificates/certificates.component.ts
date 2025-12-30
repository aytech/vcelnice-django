import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { CertificateService } from 'services';
import { FileConstants } from 'config';
import { Certificate } from 'interfaces';

@Component({
    selector: 'app-certificates',
    templateUrl: './certificates.component.html',
    styleUrls: ['./certificates.component.css'],
    standalone: false
})
export class CertificatesComponent implements OnInit {

  public certificates: Array<Certificate>;
  public loading: boolean;

  constructor(
    private certificateService: CertificateService
  ) {
    this.loading = true;
    this.certificates = [];
  }

  ngOnInit() {
    this.certificateService.getCertificates()
      .subscribe((response: Certificate[]) => {
          this.loading = false;
          this.certificates = response;
        },
        (error: HttpErrorResponse) => {
          this.loading = false;
          console.error('Error fetching data: ', error.statusText);
        });
  }

  isPdf(certificate: Certificate): boolean {
    return certificate.type === FileConstants.TYPE_PDF;
  }
}
