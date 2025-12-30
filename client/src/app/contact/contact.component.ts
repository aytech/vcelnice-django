import { Component, OnInit } from '@angular/core'
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap'

@Component({
    selector: 'app-contact',
    providers: [NgbModalConfig, NgbModal],
    styleUrls: ['./contact.component.css'],
    templateUrl: './contact.component.html',
    standalone: false
})
export class ContactComponent implements OnInit {

  constructor(config: NgbModalConfig) {
    config.backdrop = 'static'
  }

  ngOnInit() {
  }
}
