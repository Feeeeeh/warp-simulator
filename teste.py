class WarpSimulator:
    def __init__(self):
        self.standard_possible_results = [
            "imagens/bronya_pull.png", "imagens/clara_pull.png", "imagens/gepard_pull.png", 
            "imagens/himeko_pull.png", "imagens/welt_pull.png", "imagens/yanqing_pull.png", "imagens/bailu_pull"
        ]
        self.results_mapping = {
            "imagens/bronya_pull.png": "Bronya",
            "imagens/clara_pull.png": "Clara",
            "imagens/gepard_pull.png": "Gepard",
            "imagens/himeko_pull.png": "Himeko",
            "imagens/welt_pull.png": "Welt",
            "imagens/yanqing_pull.png": "Yanqing",
            "imagens/bailu_pull.png": "Bailu",
            "imagens/firefly_pull.png": "Firefly",
            "imagens/firefly_cone.png": "Cone",
            "imagens/qiqi_pull.png": "Qiqi"
        }

    def get_result_name(self, image_path):
        return self.results_mapping.get(image_path, "Unknown")

# Example usage
warp_simulator = WarpSimulator()
image_path = "imagens/himeko_pull.png"
result_name = warp_simulator.get_result_name(image_path)
print(result_name)  # Output: Himeko
