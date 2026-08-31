import { ChangeDetectionStrategy, Component, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { RecipeService } from '@services'

@Component({
    selector: 'app-recipees',
    templateUrl: './recipes.component.html',
    styleUrls: ['./recipes.component.css'],
    standalone: false,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class RecipesComponent {

  private readonly recipeService = inject(RecipeService)

  readonly recipesResource = rxResource({
    stream: () => this.recipeService.getRecipes()
  })
}
