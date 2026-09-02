import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: 'khorne', pathMatch: 'full' },
  {
    path: 'khorne',
    loadChildren: () => import('./modules/khorne/khorne.module').then((module) => module.KhorneModule),
  },
  {
    path: 'kislev',
    loadChildren: () => import('./modules/kislev/kislev.module').then((module) => module.KislevModule),
  },
  { path: '**', redirectTo: 'khorne' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'enabled', anchorScrolling: 'enabled' })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
