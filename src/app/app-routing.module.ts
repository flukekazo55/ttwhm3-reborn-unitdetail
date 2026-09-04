import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './modules/home/home.component';

const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  {
    path: 'khorne',
    loadChildren: () => import('./modules/khorne/khorne.module').then((module) => module.KhorneModule),
  },
  {
    path: 'kislev',
    loadChildren: () => import('./modules/kislev/kislev.module').then((module) => module.KislevModule),
  },
  {
    path: 'cathay',
    loadChildren: () => import('./modules/cathay/cathay.module').then((module) => module.CathayModule),
  },
  {
    path: 'dwarfs',
    loadChildren: () => import('./modules/dwarfs/dwarfs.module').then((module) => module.DwarfsModule),
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'enabled', anchorScrolling: 'enabled' })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
