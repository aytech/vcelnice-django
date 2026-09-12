import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { VideoService } from '@services'
import { LightboxService } from '../shared/lightbox/lightbox.service'

@Component({
    selector: 'app-video',
    templateUrl: './video.component.html',
    styleUrls: ['./video.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class VideoComponent {

  private readonly videoService = inject(VideoService)

  readonly lightbox = inject(LightboxService)

  readonly videosResource = rxResource({
    stream: () => this.videoService.getVideos()
  })
}
