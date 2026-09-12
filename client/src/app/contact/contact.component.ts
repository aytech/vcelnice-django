import { Component, inject, OnInit } from '@angular/core'
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap'
import { LightboxService } from '../shared/lightbox/lightbox.service'

@Component({
    selector: 'app-contact',
    providers: [NgbModalConfig, NgbModal],
    styleUrls: ['./contact.component.css'],
    templateUrl: './contact.component.html',
    standalone: false
})
export class ContactComponent implements OnInit {

  readonly lightbox = inject(LightboxService)

  constructor(config: NgbModalConfig) {
    config.backdrop = 'static'
  }

  ngOnInit() {
  }
}
