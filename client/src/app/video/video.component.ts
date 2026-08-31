import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { VideoService } from '@services'

@Component({
    selector: 'app-video',
    templateUrl: './video.component.html',
    styleUrls: ['./video.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class VideoComponent {

  private readonly videoService = inject(VideoService)

  readonly videosResource = rxResource({
    stream: () => this.videoService.getVideos()
  })
}
