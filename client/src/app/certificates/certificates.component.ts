import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { CertificateService, LanguageService } from '@services'
import { FileConstants } from '@config'
import { Certificate } from '@interfaces'

@Component({
    selector: 'app-certificates',
    templateUrl: './certificates.component.html',
    styleUrls: ['./certificates.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class CertificatesComponent {

  private readonly certificateService = inject(CertificateService)
  private readonly languageService = inject(LanguageService)

  readonly cultures = this.languageService.culturesSignal
  readonly certificatesResource = rxResource({
    stream: () => this.certificateService.getCertificates()
  })

  isPdf(certificate: Certificate): boolean {
    return certificate.type === FileConstants.TYPE_PDF;
  }
}
