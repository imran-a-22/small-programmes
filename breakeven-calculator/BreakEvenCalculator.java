import java.util.Scanner;

public class BreakEvenCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Break-Even / Profit Calculator ===");

        System.out.print("Enter selling price per unit: ");
        double sellingPrice = scanner.nextDouble();

        System.out.print("Enter variable cost per unit: ");
        double variableCost = scanner.nextDouble();

        System.out.print("Enter fixed costs: ");
        double fixedCosts = scanner.nextDouble();

        System.out.print("Enter units sold: ");
        int unitsSold = scanner.nextInt();

        if (sellingPrice <= 0 || variableCost < 0 || fixedCosts < 0 || unitsSold < 0) {
            System.out.println("Invalid input. Values must be positive.");
            scanner.close();
            return;
        }

        if (sellingPrice <= variableCost) {
            System.out.println("Break-even cannot be calculated because selling price must be greater than variable cost.");
            scanner.close();
            return;
        }

        double revenue = calculateRevenue(sellingPrice, unitsSold);
        double totalVariableCost = calculateTotalVariableCost(variableCost, unitsSold);
        double totalCost = calculateTotalCost(fixedCosts, totalVariableCost);
        double profit = calculateProfit(revenue, totalCost);
        double breakEvenUnits = calculateBreakEvenUnits(fixedCosts, sellingPrice, variableCost);
        double profitMargin = calculateProfitMargin(profit, revenue);

        System.out.println("\n=== Results ===");
        System.out.printf("Revenue: £%.2f%n", revenue);
        System.out.printf("Total Cost: £%.2f%n", totalCost);
        System.out.printf("Profit / Loss: £%.2f%n", profit);
        System.out.printf("Break-Even Units: %.2f%n", breakEvenUnits);
        System.out.printf("Profit Margin: %.2f%%%n", profitMargin);

        if (profit > 0) {
            System.out.println("Status: Profit");
        } else if (profit < 0) {
            System.out.println("Status: Loss");
        } else {
            System.out.println("Status: Break-even");
        }

        scanner.close();
    }

    public static double calculateRevenue(double sellingPrice, int unitsSold) {
        return sellingPrice * unitsSold;
    }

    public static double calculateTotalVariableCost(double variableCost, int unitsSold) {
        return variableCost * unitsSold;
    }

    public static double calculateTotalCost(double fixedCosts, double totalVariableCost) {
        return fixedCosts + totalVariableCost;
    }

    public static double calculateProfit(double revenue, double totalCost) {
        return revenue - totalCost;
    }

    public static double calculateBreakEvenUnits(double fixedCosts, double sellingPrice, double variableCost) {
        return fixedCosts / (sellingPrice - variableCost);
    }

    public static double calculateProfitMargin(double profit, double revenue) {
        if (revenue == 0) {
            return 0;
        }
        return (profit / revenue) * 100;
    }
}