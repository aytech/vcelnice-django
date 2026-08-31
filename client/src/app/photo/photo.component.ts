import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { PhotoService } from '@services'

@Component({
    selector: 'app-photo',
    templateUrl: './photo.component.html',
    styleUrls: ['./photo.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PhotoComponent {

  private readonly photoService = inject(PhotoService)

  readonly photosResource = rxResource({
    stream: () => this.photoService.getPhotos()
  })
}
