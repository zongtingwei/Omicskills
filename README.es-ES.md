<div align="center">
<img src="assets/bioclaw_logo.jpg" width="300">

# Bioclaw_Skills_Hub

### Biblioteca Oficial de Habilidades [Bioclaw](https://github.com/Runchuan-BU/BioClaw) para Bioinformática y Flujos de Trabajo de Omica

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Bioclaw_Skills_Hub** es una colección pública de habilidades reutilizables para bioinformática, análisis de omica y biología computacional.

Está organizada en torno a tareas de análisis reales en lugar de herramientas aisladas, lo que facilita explorar, reutilizar y adaptar para agentes de IA, sistemas de flujos de trabajo y asistentes de investigación.

[English](README.md) | [简体中文](README.zh-CN.md)

</div>

## Contenidos

- [Descripción General](#overview)
- [Qué Encontrarás Aquí](#what-you-will-find-here)
- [Estructura del Repositorio](#repository-structure)
- [Dominios Principales](#major-domains)
- [Qué Hace Útil a Este Repositorio](#what-makes-this-repository-useful)
- [Estado del Proyecto](#project-status)
- [Cómo Usarlo](#how-to-use-it)
- [Probar Cambios en Habilidades](#testing-skill-changes)
- [Principios de Diseño](#design-principles)
- [Licencia](#license)

## Descripción General

Los flujos de trabajo de bioinformática a menudo están dispersos en pequeñas colecciones de indicaciones, notas específicas de herramientas e instrucciones puntuales para agentes.

**Bioclaw_Skills_Hub** reúne esos patrones en una estructura de repositorio más coherente. El objetivo es proporcionar una biblioteca de habilidades más fácil de curar, enrutar y reutilizar en distintos entornos de omica, incluyendo transcriptómica, análisis de célula única, epigenómica, metagenómica, proteómica, biología estructural y bioinformática general.

**Recurso externo complementario:** [Paperzilla](https://github.com/paperzilla-ai/paperzilla-skills) ([ClawHub](https://clawhub.ai/pors/paperzilla)) es un complemento útil cuando el trabajo de omica depende del monitoreo conversacional de la literatura. Actualmente admite fuentes de bioRxiv y medRxiv basadas en proyectos, puede obtener markdown de artículos para resumen y evaluación de relevancia, y tiene previsto el soporte de PubMed.

## Qué Encontrarás Aquí

- habilidades centradas en tareas para flujos de trabajo de omica comunes
- una taxonomía que agrupa habilidades por dominio de análisis principal
- referencias más detalladas para flujos de trabajo de alto valor como ChIP-seq, ATAC-seq, expresión diferencial, metagenómica, proteómica, biología estructural y análisis de célula única
- una base para construir paquetes de ejecución más pequeños para sistemas de agentes como BioClaw

## Estructura del Repositorio

```text
Bioclaw_Skills_Hub/
├── skills/
│   ├── transcriptomics/
│   ├── single-cell-and-spatial/
│   ├── epigenomics-and-regulation/
│   ├── genomics-and-variation/
│   ├── metagenomics-and-microbiome/
│   ├── proteomics-and-metabolomics/
│   ├── multi-omics-and-systems/
│   ├── core-bioinformatics/
│   └── .../
├── catalog/
├── scripts/
└── .github/workflows/
```

## Dominios Principales

- Transcriptómica
- Célula única y espacial
- Epigenómica y regulación
- Genómica y variación
- Metagenómica y microbioma
- Proteómica y metabolómica
- Multi-ómica y biología de sistemas
- Bioinformática básica

## Qué Hace Útil a Este Repositorio

- Reduce la duplicación en muchas pequeñas colecciones de habilidades al consolidarlas en una taxonomía de omica más clara.
- Mantiene las categorías de alto nivel compactas y al mismo tiempo permite habilidades especializadas de nivel inferior.
- Es adecuado tanto como biblioteca pública independiente de habilidades como repositorio fuente para paquetes de agentes derivados.

## Estado del Proyecto

Este repositorio continuará iterándose y expandiéndose con el tiempo.

Si lo encuentras útil, considera dar una estrella ⭐ al proyecto.

## Reconocimientos

Este repositorio se inspira en colecciones de habilidades anteriores, incluyendo [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills), [OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills), [claude-for-life-sciences-skills](https://www.anthropic.com/news/claude-for-life-sciences) y [bioSkills](https://github.com/GPTomics/bioSkills).

El proyecto actual reorganiza y refina esas ideas en una estructura de biblioteca más unificada orientada a la omica.

## Cómo Usarlo

- Explora `skills/` cuando quieras un punto de entrada orientado a flujos de trabajo.
- Usa `catalog/` cuando quieras la taxonomía compacta y el mapeo de fuentes.
- Reutiliza habilidades individuales de nivel inferior directamente, o cura un subconjunto más pequeño para un entorno de agente en producción.

## Probar Cambios en Habilidades

Antes de enviar cambios a `skills/`, ejecuta el pipeline de pruebas local:

```bash
python _bioclaw_test/run_tests.py
```

Solo envía actualizaciones de habilidades después de que esta prueba pase. Verifica la consistencia de la taxonomía, los enlaces markdown, las rutas absolutas del sistema de archivos y los archivos de referencia requeridos.

## Principios de Diseño

- Agrupa las habilidades por objetivos de análisis orientados al usuario, no solo por nombres de paquetes.
- Mantén las habilidades de nivel inferior accionables y fáciles de enrutar.
- Separa la orientación general de flujos de trabajo de las referencias técnicas más detalladas.
- Facilita derivar un paquete de ejecución más pequeño y de alta señal a partir de una biblioteca pública más grande.

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).
