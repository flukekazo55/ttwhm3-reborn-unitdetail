export type FactionId = 'khorne' | 'kislev';

export interface GuideTheme {
  accent: string;
  soft: string;
  border: string;
}

export interface UnitStat {
  label: string;
  value: string;
}

export interface UnitGuide {
  id: string;
  name: string;
  imageUrl: string;
  type: string;
  role: string;
  description: string;
  stats: UnitStat[];
  traits: string[];
}

export interface SkillStep {
  order: string;
  name: string;
  points: string;
  reason: string;
  iconUrl: string;
}

export interface SkillStage {
  key: string;
  title: string;
  steps: SkillStep[];
}

export interface SkillLevelPlan {
  level: number;
  skill: string;
  note: string;
}

export interface SkillBuild {
  summary: string;
  stages: SkillStage[];
  levelPlan: SkillLevelPlan[];
}

export interface LordGuide {
  id: string;
  name: string;
  tag: string;
  style: string;
  portraitUrl: string;
  summary: string;
  bestFor: string;
  armyGuidance: string;
  skillBuild: SkillBuild;
  coreUnits: UnitGuide[];
}

export interface FactionGuide {
  id: FactionId;
  name: string;
  subtitle: string;
  description: string;
  theme: GuideTheme;
  lords: LordGuide[];
  units: UnitGuide[];
}

export interface FactionGuideState {
  faction: FactionGuide | null;
  loading: boolean;
  error: string | null;
}

export interface FactionGuideViewModel {
  faction: FactionGuide | null;
  loading: boolean;
  error: string | null;
}

export interface GuideApiResponse<T> {
  message?: string;
  data?: T;
  error?: string;
}

export interface FactionGuideApiData {
  versionLabel: string;
  faction: GuideApiFaction;
}

export interface GuideApiFaction {
  id: FactionId;
  name: string;
  subtitle: string;
  description: string;
  theme: GuideTheme;
  lords: GuideApiLord[];
  units: UnitGuide[];
}

export interface GuideApiLord {
  id: string;
  name: string;
  tag: string;
  style: string;
  portraitUrl: string;
  summary: string;
  bestFor: string;
  armyGuidance: string;
  skillBuild: SkillBuild;
  coreUnitIds: string[];
}
