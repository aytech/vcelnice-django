import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { PhotoService } from 'services';
import { Photo } from 'interfaces';

@Component({
    selector: 'app-photo',
    templateUrl: './photo.component.html',
    styleUrls: ['./photo.component.css'],
    standalone: false
})
export class PhotoComponent implements OnInit {

  public photos: Array<Photo>;
  public loading: boolean;

  constructor(
    private photoService: PhotoService
  ) {
    this.loading = true;
    this.photos = [];
  }

  ngOnInit() {
    this.photoService.getPhotos()
      .subscribe((response: Photo[]) => {
          this.loading = false;
          this.photos = response;
        },
        (reason: HttpErrorResponse) => {
          this.loading = false;
          console.error('Error fetching data: ', reason.statusText);
        });
  }
}
