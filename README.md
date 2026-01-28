# VPF Turbofan Analytical Study (TFG)

Este repositorio contiene un programa analítico para explorar cómo cambian las prestaciones de
un turbofan con Ventilador de Paso Variable (VPF) al modificar:

- El ángulo de ataque/ incidencia de los álabes.
- La velocidad de operación (Mach).

El objetivo es generar gráficas relevantes para el TFG (eficiencia, empuje específico, variación
sintética de drag, y curvas de sustentación simplificadas frente a alfa), con un modelo claro y
extensible.

## Contenido
- `src/turbofan_vpf/`: modelos analíticos y utilidades.
- `scripts/run_analysis.py`: ejecuta barridos paramétricos y exporta gráficos.
- `results/`: salida de gráficas y CSV.

## Ejecución rápida

```bash
python -m pip install -e .
python scripts/run_analysis.py --mach 0.6 0.85 1.1 --alpha -2 2 6 10
```

Las gráficas se guardan en `results/`.

## Notas de modelado
Este código utiliza correlaciones analíticas simplificadas, pensadas para estudios conceptuales.
No sustituye una validación CFD ni un diseño certificado.
