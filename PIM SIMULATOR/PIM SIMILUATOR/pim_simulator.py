import numpy as np
import time

class PIM_Core:
    """
    Tek bir pPIM core'u simüle eder.
    4-bit girişler alır, LUT-based işlem yapar.
    """

    def __init__(self, technology_node=28):
        # pPIM makalesinden alınan değerler
        self.delay_ns = 0.8  # Nano Saniye
        self.power_mw = 2.7  # Miliwat
        self.lut_size = 256  # 2**8
        self.tech_node = technology_node

        # LUT initialize
        self.lut = self._build_multiplication_lut()

    def _build_multiplication_lut(self):
        """
        4-bit x 4-bit için lookup table.
        """
        lut = np.zeros((16, 16), dtype=np.uint8)
        for i in range(16):
            for j in range(16):
                lut[i, j] = i * j
        return lut
    
    # DÜZELTME: Bu fonksiyon sola çekildi (artık sınıfın bir parçası)
    def multiply_4bit(self, a, b):
        """
        LUT kullanarak 4-bit çarpma.
        Args:
            a, b: 0-15 arası integer
        Returns:
            result: Çarpım sonucu
            energy_pj: Harcanan enerji
            latency_ns: İşlem gecikmesi
        """
        # LUT'tan oku
        result = self.lut[a, b]

        # Enerji hesabı: P(mW) × t(ns) = pJ
        energy_pj = self.power_mw * self.delay_ns

        return result, energy_pj, self.delay_ns

    def add_4bit(self, a, b):
        """
        4-bit toplama.
        """
        result = (a + b) & 0xFF  # 8 bit sonuç
        
        # DÜZELTME: 'energy.pj' yazım hatası 'energy_pj' yapıldı
        energy_pj = self.power_mw * self.delay_ns

        return result, energy_pj, self.delay_ns

    def multiply_8bit_approx_4bit(self, a, b):
        """
        8-bit sayıları 4-bit LUT ile yaklaşık çarpma.
        """
        # Sayıları 4-bit parçalara böl
        a_high = (a >> 4) & 0xF  # Üst 4 bit
        a_low = a & 0xF          # Alt 4 bit
        b_high = (b >> 4) & 0xF
        b_low = b & 0xF
    
        # DÜZELTME: Aşağıdaki satırların girintisi düzeltildi
        # 4 adet 4-bit çarpma (LUT kullanarak)
        V0, e0, l0 = self.multiply_4bit(a_low, b_low)
        V1, e1, l1 = self.multiply_4bit(a_low, b_high)
        V2, e2, l2 = self.multiply_4bit(a_high, b_low)
        V3, e3, l3 = self.multiply_4bit(a_high, b_high)
    
        # Sonuçları birleştir
        result = int(V0) + (int(V1) << 4) + (int(V2) << 4) + (int(V3) << 8)
    
        # Toplam enerji ve gecikme
        total_energy = e0 + e1 + e2 + e3
        total_latency = max(l0, l1, l2, l3) 
    
        return result, total_energy, total_latency

class PIMCluster():
    """
    
    9 core(Çekirdek) dan oluşturuyoruz
    
    ÇÜNKÜ:8-bitlik bir çarpma işlemini, 4-bitlik donanımla simüle etmek için işlemi parçalara ayırdıklarında, 
    bu parçaları paralel işleyip birleştirmek için en uygun geometrik ve sayısal yapı 3 x 3 = 9 çekirdekli bir kümedir.

    """
    def __init__(self, technology_node=28):
        self.cores = [PIM_Core(technology_node) for _ in range(9)]

        #pPIM: A Programmable Processor-in-Memory Architecture With Precision-Scaling for Deep Learning 
        # makalesindeki alınan Cluster-level özellikler 

        self.mac_delay_ns = 6.4 # 8 stage işlme
        self.mac_power = 5.2
        self.router_overhead = 0.5 #Corelar arası iletişim

    def mac_8bit(self, a_8bit, b_8bit, accumulator=0, precision=8):
         """
        8-bit Multiply-Accumulate işlemi.
        
        İşlem adımları (pPIM paper Fig. 2):
        1. 8-bit sayıları 4-bit'lere böl: aH, aL, bH, bL
        2. Partial products: V0=aLxbL, V1=aLxbH, V2=aHxbL, V3=aHxbH
        3. 8 stage'de topla
        
        Args:
            a_8bit, b_8bit: 0-255 arası integer
            accumulator: Önceki sonuç (MAC'te kullanılır)
            precision: 8 veya 4 (precision scaling için)
        
        Returns:
            result: MAC sonucu
            total_energy_pj: Toplam enerji
            total_latency_ns: Toplam gecikme
        """
         
         total_energy = 0
         total_latency = 0

         if precision == 8:
            # 8-bit tam hassasiyet
            aH, aL = (a_8bit >> 4) & 0xF, a_8bit & 0xF
            bH, bL = (b_8bit >> 4) & 0xF, b_8bit & 0xF
            
            # Stage 1-4: Partial products (4 core çarpma yapar)
            V0, e0, l0 = self.cores[0].multiply_4bit(aL, bL)
            V1, e1, l1 = self.cores[1].multiply_4bit(aL, bH)
            V2, e2, l2 = self.cores[2].multiply_4bit(aH, bL)
            V3, e3, l3 = self.cores[3].multiply_4bit(aH, bH)
            
            # Stage 5-8: Accumulation (5 core toplama yapar)
            # Basitleştirilmiş: gerçekte daha karmaşık bit-shifting var
            result = int(V0) + (int(V1) << 4) + (int(V2) << 4) + (int(V3) << 8)
            result += accumulator
            
            # Enerji: 4 multiply + 5 add + router overhead
            total_energy = (e0 + e1 + e2 + e3) + (5 * self.cores[0].power_mw * 0.8)
            total_latency = self.mac_delay_ns  # Pipeline olarak 8 stage
            
        
         elif precision == 4:
            # 4-bit precision scaling (pPIM: A Programmable Processor-in-Memory Architecture 
            # With Precision-Scaling for Deep Learning  Fig. 2 - approximate)
            
            # Sadece en önemli 4 biti kullan
             aH = (a_8bit >> 4) & 0xF
             bH = (b_8bit >> 4) & 0xF
             
             # Tek çarpma + tek toplama yeter
             V3, e3, l3 = self.cores[0].multiply_4bit(aH, bH)
             result = (V3 << 8) + accumulator
            
            # Enerji: 1 multiply + 1 add (papPIM: A Programmable Processor-in-Memory Architecture 
            # With Precision-Scaling for Deep Learning per'da 1.35x tasarruf)
             
             total_energy = e3 + (self.cores[0].power_mw * 0.8)
             total_latency = 3.2  # Yarı süre (4 stage yerine 2)
         else:
            raise ValueError("Precision 4 veya 8 olmalı")
        
         return int(result) & 0xFFFF, total_energy, total_latency

class PIMArray:
    """
    256 cluster'dan oluşan tam PIM chip simülasyonu.
    """
    def __init__(self, num_clusters=256, technology_node=28):
        self.clusters = [PIMCluster(technology_node) for _ in range(num_clusters)]
        self.num_clusters = num_clusters



        # Memory communication (pPIM: A Programmable Processor-in-Memory Architecture 
        # With Precision-Scaling for Deep Learning Table 1)
        # Memory communication (paper Table 1)
        self.intra_subarray_energy_uj = 0.028  # RowClone
        self.intra_subarray_latency_ns = 63.0
        
        self.inter_subarray_energy_uj = 0.09  # LISA (1 hop)
        self.inter_subarray_latency_ns = 148.5

    def convolution_layer(self, input_shape, kernel_shape, precision=8):
        """
        Bir CNN katmanını simüle eder.
        
        Args:
            input_shape: (C_in, H, W)
            kernel_shape: (C_out, C_in, Kh, Kw)
            precision: 8 veya 4 bit
        
        Returns:
            stats: Enerji ve gecikme istatistikleri
        """

        C_out, C_in, Kh, Kw = kernel_shape
        _, H, w = input_shape

        #Her output pixel için gereken MAC sayısı

        macs_per_output = C_in * Kh * Kw

        #Toplam output pixel için gereken MAC sayısı
        out_H = H - Kh + 1 
        out_W = w - Kh + 1
        total_outputs  = C_out * out_H * out_W 

        # Toplam MAC işlemi
        total_macs = total_outputs * macs_per_output
         
        #PIM clusterlara dağıt(parallelization)
        macs_per_cluster = total_macs // self.num_clusters


        #Tek bir mac maliyet hesabı 
        dummy_cluster = self.clusters[0]
        _ , mac_energy_pj, mac_latency = dummy_cluster.mac_8bit(128, 128, 0, precision)

        ## Toplam computation cost
        total_energy_compute_mj = (total_macs * mac_energy_pj) / 1e9  # pJ -> mJ

        # Memory communication cost
        # Varsayım: Her cluster kendi subarray'inde (intra-subarray comm.)
        total_comm_energy_mj = (macs_per_cluster * self.intra_subarray_energy_uj) / 1e3

        # Latency (parallelization sayesinde)
        total_latency_ms = (macs_per_cluster * mac_latency) / 1e6  # ns -> ms
        return {
            'precision': precision,
            'total_macs': total_macs,
            'latency_ms': total_latency_ms,
            'energy_compute_mj': total_energy_compute_mj,
            'energy_communication_mj': total_comm_energy_mj,
            'energy_total_mj': total_energy_compute_mj + total_comm_energy_mj,
            'power_mw': (total_energy_compute_mj + total_comm_energy_mj) / (total_latency_ms / 1000),
        }
    
    
    def model_inference(self, layer_configs, precision=8):
        """
        Tüm CNN modelini simüle eder.
        
        Args:
            layer_configs: Her katmanın (input_shape, kernel_shape) tuple'ları
            precision: 8 veya 4 bit
        
        Returns:
            total_stats: Toplam enerji/gecikme
        """
        total_energy = 0
        total_latency = 0
        total_macs = 0

        for input_shape, kernel_shape in layer_configs:
            stats = self.convolution_layer(input_shape, kernel_shape, precision)
            total_energy += stats['energy_total_mj']
            total_latency += stats['latency_ms']
            total_macs += stats['total_macs']
        
        return {
            'total_energy_mj': total_energy,
            'total_latency_ms': total_latency,
            'total_macs': total_macs,
            'avg_power_mw': total_energy / (total_latency / 1000) if total_latency > 0 else 0,
            'precision': precision
        }
































