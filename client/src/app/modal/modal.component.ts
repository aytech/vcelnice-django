import { Component, TemplateRef, ViewChild } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.css']
})
export class ModalComponent {
  @ViewChild('content') private content: TemplateRef<any>;
  public title: string;
  public body: string;

  constructor(private modalService: NgbModal) {
  }

  open(title: string, body: string): void {
    this.title = title;
    this.body = body;
    this.modalService
      .open(this.content)
      .result.then(() => {
      // Not used
    }, () => {
      // Modal dismissed
    });
  }
}
