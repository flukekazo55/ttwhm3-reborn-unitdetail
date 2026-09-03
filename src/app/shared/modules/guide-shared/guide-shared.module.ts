import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { TagModule } from 'primeng/tag';
import { GuideLordDetailComponent } from './guide-lord-detail.component';
import { GuideLordSelectComponent } from './guide-lord-select.component';
import { GuideLordComponent } from './guide-lord.component';
import { GuideSkillBuildComponent } from './guide-skill-build.component';
import { GuideUnitCardComponent } from './guide-unit-card.component';

@NgModule({
  declarations: [
    GuideLordSelectComponent,
    GuideLordDetailComponent,
    GuideLordComponent,
    GuideSkillBuildComponent,
    GuideUnitCardComponent,
  ],
  imports: [CommonModule, RouterModule, TagModule],
  exports: [
    GuideLordSelectComponent,
    GuideLordDetailComponent,
    GuideLordComponent,
    GuideSkillBuildComponent,
    GuideUnitCardComponent,
  ],
})
export class GuideSharedModule {}
