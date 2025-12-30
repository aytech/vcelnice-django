import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { VideoService } from 'services';
import { Video } from 'interfaces';

@Component({
    selector: 'app-video',
    templateUrl: './video.component.html',
    styleUrls: ['./video.component.css'],
    standalone: false
})
export class VideoComponent implements OnInit {

  public videos: Array<Video>;
  public loading: boolean;

  constructor(
    private videoService: VideoService
  ) {
    this.loading = true;
    this.videos = [];
  }

  ngOnInit() {
    this.videoService.getVideos()
      .subscribe((data: Video[]) => {
          this.loading = false;
          this.videos = data;
        },
        (error: HttpErrorResponse) => {
          this.loading = false;
          console.error('Error fetching data: ', error.statusText);
        });
  }
}
