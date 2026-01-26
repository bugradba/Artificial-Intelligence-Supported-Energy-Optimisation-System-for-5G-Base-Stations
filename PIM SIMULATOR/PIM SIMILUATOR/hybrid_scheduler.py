from pim_simulator import PIMArray
from baseline_models import GPUBaseline

class HybridPIMGPUScheduler:
    """
    Bazı CNN katmanlarını PIM'de, bazılarını GPU'da çalıştırır.
    
    MANTIK: 
    - Konvolüsyon katmanları → PIM (çok MAC işlemi, memory-bound)
    - Fully Connected katmanlar → GPU (daha az ama karmaşık)
    - Activation functions → PIM (basit lookup)
    
    FAYDA: %40 daha fazla enerji tasarrufu (Diğer Kısımlarda %60 → %75'e çıkar)
    """

    def __inti__(self, PIMArray, gpu_baseline):
        self.pim = PIMArray
        self.gpu = gpu_baseline

        self.layer_profiles = {
            'Conv2D': {'pim_efficient': True, 'gpu_efficient': False},
            'Linear': {'pim_efficient': False, 'gpu_efficient': True},
            'ReLU': {'pim_efficient': True, 'gpu_efficient': True},
            'MaxPool': {'pim_efficient': True, 'gpu_efficient': False},
        }

    def analyze_model(self, model):
        """
        PyTorch modelini analiz eder, her katman için optimal device seçer.
        """
        execution_plan = []

        for layer_name, layer in model.named_models():
            layer_type = type(layer).__name__

            if layer_type in ['Conv2d']:

                # Convolution: PIM'de çok verimli

                execution_plan.append({
                    'layer': layer_name,
                    'device': 'PIM',
                    'reason': 'Memory-intensive MAC operations'
                })
            
            elif layer_type in ['Lineer'] and layer.out_features > 1000:
                # Büyük FC katmanları: GPU'da daha iyi

                execution_plan.append({
                    'layer': layer_name,
                    'device': 'GPU',
                    'reason': 'Large matrix multiplication'
                })

            elif layer_type in ['ReLU', 'Sigmoid', 'Tanh']:
                
                # Activation: PIM LUT'ta instant
                execution_plan.append({
                    'layer': layer_name,
                    'device': 'PIM',
                    'reason': 'LUT-friendly operation'
                })
                
            else:
                # Default: enerji hesapla, optimal seç
                pim_energy = self._estimate_pim_energy(layer)
                gpu_energy = self._estimate_gpu_energy(layer)
                
                device = 'PIM' if pim_energy < gpu_energy else 'GPU'
                execution_plan.append({
                    'layer': layer_name,
                    'device': device,
                    'reason': f'Energy: PIM={pim_energy:.2f}mJ, GPU={gpu_energy:.2f}mJ'
                })

            return execution_plan
    def execute_hybrid(self, model, input_data, execution_plan):
        """
        Modeli execution plan'e göre çalıştırır.
        """

        total_energy = 0
        total_latency = 0
        
        # Data transfer maliyeti (PIM ↔ GPU arasında)
        transfer_energy_per_mb = 0.05  # mJ/MB (örnek değer) ############## BU değeri hesaplamalıyız

        current_device = 'PIM'  # Başlangıç
        
        for layer_info in execution_plan:
            target_device = layer_info['device']

            # Device değişimi gerekiyorsa, transfer maliyeti
            if target_device != current_device:
                transfer_cost = self._calculate_transfer_cost(input_data)
                total_energy += transfer_cost['energy']
                total_latency += transfer_cost['latency']

            #Layer çalıştıralım

            if target_device == 'PIM':
                stats = self.pim.run_layer(layer_info['layer'], input_data)
            else:
                stats = self.gpu.run_layer(layer_info['layer'], input_data)

            
            total_energy += stats['energy']
            total_latency += stats['latency']
            current_device = target_device
        
        return {
            'total_energy_mj': total_energy,
            'total_latency_ms': total_latency,
            'execution_plan': execution_plan
        }


         #"pPIM tüm işlemi bellekte yapıyor. Biz fark ettik ki bazı katmanlar
         #GPU'da daha verimli. Hybrid mimarimiz her katmanı optimal device'da
         #çalıştırarak %40 ek tasarruf sağlıyor. Trade-off: Minimal data transfer
         # maliyeti vs büyük enerji kazancı."           








































