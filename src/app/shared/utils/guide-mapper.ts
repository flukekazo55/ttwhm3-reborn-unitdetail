import {
  FactionGuide,
  GuideApiFaction,
  LordGuide,
  UnitGuide,
} from '../models/guide.model';

export function toFactionGuide(faction: GuideApiFaction): FactionGuide {
  const unitMap = new Map<string, UnitGuide>(faction.units.map((unit) => [unit.id, unit]));
  const lords: LordGuide[] = faction.lords.map((lord) => ({
    id: lord.id,
    name: lord.name,
    tag: lord.tag,
    style: lord.style,
    portraitUrl: lord.portraitUrl,
    summary: lord.summary,
    bestFor: lord.bestFor,
    armyGuidance: lord.armyGuidance,
    skillBuild: lord.skillBuild,
    coreUnits: lord.coreUnitIds
      .map((unitId) => unitMap.get(unitId))
      .filter((unit): unit is UnitGuide => unit !== undefined),
  }));

  return {
    id: faction.id,
    name: faction.name,
    subtitle: faction.subtitle,
    description: faction.description,
    theme: faction.theme,
    lords,
    units: faction.units,
  };
}
