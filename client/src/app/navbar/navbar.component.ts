import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  ElementRef,
  inject,
  OnInit,
  ViewChild
} from '@angular/core'
import { NavigationEnd, Router } from '@angular/router'
import { takeUntilDestroyed } from '@angular/core/rxjs-interop'
import { filter } from 'rxjs'
import { LanguageService } from '@services'

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarComponent implements OnInit {

  @ViewChild('navbarToggle') navbarToggle?: ElementRef<HTMLButtonElement>
  @ViewChild('menu') menu?: ElementRef<HTMLElement>

  private readonly router = inject(Router)
  private readonly destroyRef = inject(DestroyRef)
  private readonly languageService = inject(LanguageService)

  readonly locale = this.languageService.localeSignal
  readonly cultures = this.languageService.culturesSignal

  ngOnInit(): void {
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(() => {
      if (this.isMenuOpen()) {
        this.navbarToggle?.nativeElement.click()
      }
    })
  }

  private isMenuOpen(): boolean {
    return this.menu?.nativeElement.offsetParent != null
  }
}
