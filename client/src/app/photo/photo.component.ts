import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { PhotoService } from '@services'
import { LightboxService } from '../shared/lightbox/lightbox.service'

@Component({
    selector: 'app-photo',
    templateUrl: './photo.component.html',
    styleUrls: ['./photo.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PhotoComponent {

  private readonly photoService = inject(PhotoService)

  readonly lightbox = inject(LightboxService)
  readonly previewLimit = 8

  readonly photosResource = rxResource({
    stream: () => this.photoService.getPhotos()
  })
}
