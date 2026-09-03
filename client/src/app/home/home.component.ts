import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap'
import { HomeService } from '@services'

@Component({
    selector: 'app-home',
    providers: [NgbModalConfig, NgbModal],
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit {

  private readonly homeService = inject(HomeService)

  readonly homeResource = rxResource({
    stream: () => this.homeService.getText()
  })

  ngOnInit(): void {}
}
